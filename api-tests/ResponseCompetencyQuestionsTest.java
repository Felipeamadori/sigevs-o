package br.com.pdsars.sigevs.competency;

import br.com.pdsars.sigevs.dto.ResponseBarrierDTO;
import br.com.pdsars.sigevs.dto.ResponseCommandPostDTO;
import br.com.pdsars.sigevs.dto.ResponseSurveillanceCycleDTO;
import br.com.pdsars.sigevs.dto.ResponseVehicleDTO;
import br.com.pdsars.sigevs.dto.ResponseAreaDTO;
import br.com.pdsars.sigevs.dto.ResponseConvokedUsersDTO;
import br.com.pdsars.sigevs.dto.TeamTrackingDTO;
import br.com.pdsars.sigevs.enums.ResponseBarrierRole;
import br.com.pdsars.sigevs.enums.ResponseBarrierType;
import br.com.pdsars.sigevs.exception.UnprocessableEntityException;
import br.com.pdsars.sigevs.mappers.ResponseBarrierMapper;
import br.com.pdsars.sigevs.mappers.ResponseCommandPostMapper;
import br.com.pdsars.sigevs.mappers.ResponseConvokedUsersMapper;
import br.com.pdsars.sigevs.mappers.ResponseSurveillanceCycleMapper;
import br.com.pdsars.sigevs.mappers.ResponseVehicleMapper;
import br.com.pdsars.sigevs.mappers.ResponseAreaMapper;
import br.com.pdsars.sigevs.mappers.TeamTrackingMapper;
import br.com.pdsars.sigevs.model.*;
import br.com.pdsars.sigevs.model.registration.Usuario;
import br.com.pdsars.sigevs.repository.*;
import br.com.pdsars.sigevs.repository.registration.UsuarioRepository;
import br.com.pdsars.sigevs.service.*;
import jakarta.persistence.EntityNotFoundException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.lang.reflect.Field;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the Sanitary Response subdomain competency questions
 * (CQ-RES-01..14). One test per competency question; all collaborators are
 * mocked (no database).
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ResponseCompetencyQuestionsTest {

    @Mock private ResponseSurveillanceCycleRepository responseSurveillanceCycleRepository;
    @Mock private ResponseAreaRepository responseAreaRepository;
    @Mock private SanitaryEventResponseRepository sanitaryEventResponseRepository;
    @Mock private ResponseTeamRepository responseTeamRepository;
    @Mock private SysEventLoggerService sysEventLoggerService;
    @Mock private ResponseSurveillanceCycleMapper responseSurveillanceCycleMapper;
    @Mock private SanitaryAnalysisRepository sanitaryAnalysisRepository;
    @Mock private SurveillanceCycleZoneRepository surveillanceCycleZoneRepository;
    @Mock private PremiseSubmissionRepository premiseSubmissionRepository;
    @Mock private AffectedAreaRepository affectedAreaRepository;

    @Mock private ResponseBarrierRepository responseBarrierRepository;
    @Mock private ResponseBarrierMapper responseBarrierMapper;
    @Mock private ResponseVehicleRepository responseVehicleRepository;
    @Mock private ResponseVehicleMapper responseVehicleMapper;
    @Mock private ResponseCommandPostRepository responseCommandPostRepository;
    @Mock private ResponseCommandPostMapper responseCommandPostMapper;
    @Mock private TeamTrackingRepository teamTrackingRepository;
    @Mock private TeamTrackingMapper teamTrackingMapper;
    @Mock private ResponseAreaMapper responseAreaMapper;
    @Mock private ResponseConvokedUsersRepository responseConvokedUsersRepository;
    @Mock private br.com.pdsars.sigevs.service.registration.UsuarioService usuarioService;

    @InjectMocks private ResponseSurveillanceCycleService cycleService;
    @InjectMocks private ResponseBarrierService barrierService;
    @InjectMocks private ResponseVehicleService vehicleService;
    @InjectMocks private ResponseCommandPostService commandPostService;
    @InjectMocks private TeamTrackingService teamTrackingService;
    @InjectMocks private ResponseAreaService areaService;
    @InjectMocks private EventActionsService eventActionsService;

    private final ResponseConvokedUsersMapper convokedMapper = new ResponseConvokedUsersMapper();
    private ResponseConvokedUsersService convokedService;

    @org.junit.jupiter.api.BeforeEach
    void setUp() {
        convokedService = new ResponseConvokedUsersService(
                responseConvokedUsersRepository, sanitaryEventResponseRepository,
                mock(br.com.pdsars.sigevs.repository.registration.UsuarioRepository.class),
                convokedMapper, mock(ResponseRolesRepository.class),
                responseTeamRepository, mock(TeamMemberRepository.class));
    }

    @Test
    @DisplayName("CQ-RES-01 — Quantos/quais ciclos de vigilância foram executados em uma resposta?")
    void cqRes01() {
        UUID uuid = UUID.randomUUID();
        ResponseSurveillanceCycle c1 = new ResponseSurveillanceCycle();
        c1.setCycleNumber(1);
        ResponseSurveillanceCycle c2 = new ResponseSurveillanceCycle();
        c2.setCycleNumber(2);
        when(responseSurveillanceCycleRepository.findAllBySanitaryEventResponseUuidOrderByCycleNumberAsc(uuid))
                .thenReturn(List.of(c1, c2));
        when(responseSurveillanceCycleMapper.toDto(any())).thenAnswer(inv -> {
            ResponseSurveillanceCycle cycle = inv.getArgument(0);
            ResponseSurveillanceCycleDTO dto = new ResponseSurveillanceCycleDTO();
            dto.setCycleNumber(cycle.getCycleNumber());
            return dto;
        });

        List<ResponseSurveillanceCycleDTO> cycles = cycleService.findAllByFocusResponseUuid(uuid);

        assertEquals(2, cycles.size());
        assertEquals(1, cycles.get(0).getCycleNumber());
        assertEquals(2, cycles.get(1).getCycleNumber());
    }

    @Test
    @DisplayName("CQ-RES-02 — Quais equipes estão alocadas em cada ciclo de vigilância?")
    void cqRes02() {
        ResponseSurveillanceCycle cycle = new ResponseSurveillanceCycle();
        ResponseTeam team = new ResponseTeam();
        team.setTeamName("Equipe A");
        team.setResponseSurveillanceCycle(cycle);

        assertSame(cycle, team.getResponseSurveillanceCycle());
        assertEquals("Equipe A", team.getTeamName());
    }

    @Test
    @DisplayName("CQ-RES-03 — Quais profissionais compõem cada equipe e qual sua função?")
    void cqRes03() {
        ResponseTeam team = new ResponseTeam();
        TeamMember member = new TeamMember();
        Usuario user = new Usuario();
        user.setNome("Joao Silva");
        member.setUser(user);
        team.addTeamMember(member);

        assertEquals(1, team.getTeamMembers().size());
        assertSame(team, member.getTeam());
        assertEquals("Joao Silva", team.getTeamMembers().get(0).getUser().getNome());
    }

    @Test
    @DisplayName("CQ-RES-04 — Uma barreira pertence a um ciclo por vez (novas barreiras por ciclo)")
    void cqRes04() {
        ResponseSurveillanceCycle cycle = new ResponseSurveillanceCycle();
        ResponseBarrier barrier = new ResponseBarrier();
        barrier.setBarrierName("Barreira BR-287");
        barrier.setSurveillanceCycle(cycle);

        assertSame(cycle, barrier.getSurveillanceCycle(),
                "each cycle gets its own barrier records (no cross-cycle sharing)");
    }

    @Test
    @DisplayName("CQ-RES-05 — Uma nova ZonaPorCiclo é criada por ciclo (replicação não reusa dados)")
    void cqRes05() {
        UUID uuid = UUID.randomUUID();
        var options = new br.com.pdsars.sigevs.dto.CycleReplicationOptionsDTO(true, false, false, false);

        // replication targets cycles after cycle 1
        assertThrows(br.com.pdsars.sigevs.exception.BadRequestException.class,
                () -> cycleService.replicateData(uuid, 1, options));

        when(responseSurveillanceCycleRepository.findBySanitaryEventResponseUuidAndCycleNumber(uuid, 2))
                .thenReturn(Optional.of(new ResponseSurveillanceCycle()));
        when(responseTeamRepository.existsByResponseSurveillanceCycleId(any())).thenReturn(true);

        // a cycle that already has data is not repopulated: zones/teams are per cycle
        assertThrows(UnprocessableEntityException.class,
                () -> cycleService.replicateData(uuid, 2, options));
    }

    @Test
    @DisplayName("CQ-RES-06 — Qual o histórico de rastreamento GPS das equipes?")
    void cqRes06() {
        when(teamTrackingRepository.findByTeamId(1L)).thenReturn(List.of(new TeamTracking(), new TeamTracking()));
        when(teamTrackingMapper.toDTO(any(TeamTracking.class))).thenReturn(new TeamTrackingDTO());

        TeamTrackingService trackingService = new TeamTrackingService(teamTrackingRepository, teamTrackingMapper);
        List<TeamTrackingDTO> trackings = trackingService.findByTeamId(1L);

        assertEquals(2, trackings.size());
    }

    @Test
    @DisplayName("CQ-RES-07 — Uma equipe pertence a um único ciclo por vez (estrutural)")
    void cqRes07() {
        long cycleFields = java.util.Arrays.stream(ResponseTeam.class.getDeclaredFields())
                .map(Field::getType)
                .filter(type -> type == ResponseSurveillanceCycle.class)
                .count();
        assertEquals(1, cycleFields,
                "ResponseTeam has a single cycle FK: a team is allocated to one cycle at a time");
    }

    @Test
    @DisplayName("CQ-RES-08 — Quais áreas operacionais foram atribuídas a cada equipe?")
    void cqRes08() {
        when(responseAreaRepository.findByTeamId(1L)).thenReturn(List.of(new ResponseArea(), new ResponseArea()));
        when(responseAreaMapper.toDTO(any(ResponseArea.class))).thenReturn(new ResponseAreaDTO());

        List<ResponseAreaDTO> areas = areaService.findByTeamId(1L);

        assertEquals(2, areas.size());
    }

    @Test
    @DisplayName("CQ-RES-09 — Quais barreiras sanitárias estão ativas em uma resposta?")
    void cqRes09() {
        UUID uuid = UUID.randomUUID();
        ResponseBarrier barrier = new ResponseBarrier();
        barrier.setBarrierName("Barreira BR-287");
        when(responseBarrierRepository.findByFocusResponseUuid(uuid)).thenReturn(List.of(barrier));
        when(responseBarrierMapper.toDTO(barrier)).thenReturn(new ResponseBarrierDTO());

        List<ResponseBarrierDTO> barriers = barrierService.findByFocusResponseUuid(uuid);

        assertEquals(1, barriers.size());
    }

    @Test
    @DisplayName("CQ-RES-10 — Quais propriedades estão atribuídas a cada área operacional?")
    void cqRes10() {
        UUID uuid = UUID.randomUUID();
        SanitaryEventResponse response = mock(SanitaryEventResponse.class);
        when(response.getIsActive()).thenReturn(true);
        when(sanitaryEventResponseRepository.findByUuid(uuid)).thenReturn(Optional.of(response));
        when(response.getId()).thenReturn(5L);
        when(sanitaryAnalysisRepository.findAllocatedPremisesInTargetZones(5L))
                .thenReturn(List.of(mock(br.com.pdsars.sigevs.dto.projection.PremiseProjection.class)));

        var premises = eventActionsService.findAllocatedPremises(uuid);

        assertEquals(1, premises.size());
        verify(sanitaryAnalysisRepository).findAllocatedPremisesInTargetZones(5L);
    }

    @Test
    @DisplayName("CQ-RES-11 — Qual o tipo (fixo/móvel) e função (sanitária/desvio) da barreira?")
    void cqRes11() {
        ResponseBarrier barrier = new ResponseBarrier();
        barrier.setType(ResponseBarrierType.FIXED);
        barrier.setRole(ResponseBarrierRole.SANITARY);

        assertEquals(ResponseBarrierType.FIXED, barrier.getType());
        assertEquals("Posto Fixo", barrier.getType().getLabel());
        assertEquals(ResponseBarrierRole.SANITARY, barrier.getRole());
        assertEquals("Barreira Sanitária", barrier.getRole().getLabel());
    }

    @Test
    @DisplayName("CQ-RES-12 — Quais veículos estão alocados a cada equipe?")
    void cqRes12() {
        when(responseVehicleRepository.findByTeamId(1L)).thenReturn(List.of(new ResponseVehicle()));
        when(responseVehicleMapper.toDTO(any(ResponseVehicle.class))).thenReturn(new ResponseVehicleDTO());

        List<ResponseVehicleDTO> vehicles = vehicleService.findByTeamId(1L);

        assertEquals(1, vehicles.size());
    }

    @Test
    @DisplayName("CQ-RES-13 — Onde está localizado o posto de comando da resposta?")
    void cqRes13() {
        UUID uuid = UUID.randomUUID();
        when(responseCommandPostRepository.findBySanitaryEventResponseUuid(uuid))
                .thenReturn(Optional.of(new ResponseCommandPost()));
        when(responseCommandPostMapper.toDto(any(ResponseCommandPost.class)))
                .thenReturn(new ResponseCommandPostDTO());

        ResponseCommandPostDTO post = commandPostService.findByFocusResponseUuid(uuid);

        assertNotNull(post);
    }

    @Test
    @DisplayName("CQ-RES-14 — Quais profissionais foram convocados e qual seu status de quarentena?")
    void cqRes14() {
        UUID uuid = UUID.randomUUID();
        SanitaryEventResponse response = new SanitaryEventResponse();
        when(sanitaryEventResponseRepository.findByUuid(uuid)).thenReturn(Optional.of(response));

        ResponseConvokedUsers summoned = ResponseConvokedUsers.builder().build();
        summoned.setIsDirty(false);
        summoned.setIsActive(true);
        summoned.setIsManagement(true);
        summoned.setIsObserver(false);
        Usuario user = new Usuario();
        user.setIdUsuario(7);
        user.setNome("Joao Silva");
        summoned.setUser(user);
        when(responseConvokedUsersRepository.findBySanitaryEventResponse(response))
                .thenReturn(List.of(summoned));

        List<ResponseConvokedUsersDTO> result = convokedService.findByFocusResponseUuid(uuid);

        assertEquals(1, result.size());
        assertFalse(result.get(0).getIsDirty(), "quarantine status exposed (dirty=false)");
        assertTrue(result.get(0).getIsManagement());
        assertEquals("Joao Silva", result.get(0).getUserName());
    }
}
