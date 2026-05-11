import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const sessoes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sessoes' }),
  schema: z.object({
    titulo: z.string(),
    data: z.coerce.date(),
    numero: z.number(),
    tema: z.string(),
    sumario: z.string(),
    desfecho: z.enum(['acordo-provavel', 'impasse', 'consenso']).optional(),
    partidos: z.array(z.string()),
    quinzenal_link: z.string().optional(),
    quick_facts: z
      .array(
        z.object({
          label: z.string(),
          value: z.string(),
        }),
      )
      .optional(),
    posicoes: z
      .array(
        z.object({
          partido: z.string(),
          deputados: z.number(),
          frase: z.string(),
        }),
      )
      .optional(),
    cenarios: z
      .object({
        provavel: z.object({
          titulo: z.string(),
          geometria: z.string(),
          sumario: z.string(),
          chave: z.string().optional(),
        }),
        consenso: z.object({
          titulo: z.string(),
          geometria: z.string(),
          sumario: z.string(),
          chave: z.string().optional(),
        }),
        impasse: z.object({
          titulo: z.string(),
          geometria: z.string(),
          sumario: z.string(),
          chave: z.string().optional(),
        }),
      })
      .optional(),
    takeaway: z.string().optional(),
  }),
});

export const collections = { sessoes };
